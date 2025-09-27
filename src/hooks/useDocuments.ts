import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';

export const useDocuments = (ownerScope: string, ownerId: string) => {
  return useQuery({
    queryKey: ['documents', ownerScope, ownerId],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('documents')
        .select('*')
        .eq('owner_scope', ownerScope)
        .eq('owner_id', ownerId)
        .order('created_at', { ascending: false });
      
      if (error) throw error;
      return data;
    },
  });
};

export const useUploadDocument = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ file, ownerScope, ownerId }: { file: File; ownerScope: string; ownerId: string }) => {
      // Upload file to storage
      const fileName = `${Date.now()}_${file.name}`;
      const { data: uploadData, error: uploadError } = await supabase.storage
        .from('documents')
        .upload(fileName, file);
      
      if (uploadError) throw uploadError;
      
      // Create document record
      const { data, error } = await supabase
        .from('documents')
        .insert({
          owner_scope: ownerScope,
          owner_id: ownerId,
          filename: file.name,
          content_type: file.type,
          storage_path: uploadData.path,
          source_type: file.type.includes('pdf') ? 'pdf' : 
                      file.type.includes('word') ? 'docx' : 
                      file.type.includes('image') ? 'image' : 'other',
        })
        .select()
        .single();
      
      if (error) throw error;
      return data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['documents', variables.ownerScope, variables.ownerId] });
    },
  });
};

export const useDeleteDocument = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (documentId: string) => {
      // Get document to delete storage file
      const { data: document, error: fetchError } = await supabase
        .from('documents')
        .select('storage_path')
        .eq('id', documentId)
        .single();
      
      if (fetchError) throw fetchError;
      
      // Delete storage file
      const { error: deleteError } = await supabase.storage
        .from('documents')
        .remove([document.storage_path]);
      
      if (deleteError) throw deleteError;
      
      // Delete document record
      const { data, error } = await supabase
        .from('documents')
        .delete()
        .eq('id', documentId);
      
      if (error) throw error;
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};