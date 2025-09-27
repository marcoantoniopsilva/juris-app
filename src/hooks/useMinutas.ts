import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';

export const useCreateMinuta = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (minutaData: any) => {
      const { data, error } = await supabase
        .from('minutas')
        .insert(minutaData)
        .select()
        .single();
      
      if (error) throw error;
      return data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['minutas', variables.case_id] });
    },
  });
};

export const useUpdateMinuta = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (minutaData: any) => {
      const { data, error } = await supabase
        .from('minutas')
        .update(minutaData)
        .eq('id', minutaData.id);
      
      if (error) throw error;
      return data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['minutas', variables.case_id] });
    },
  });
};

export const useDeleteMinuta = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (minutaId: string) => {
      const { data, error } = await supabase
        .from('minutas')
        .delete()
        .极('id', minutaId);
      
      if (error) throw error;
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['minutas'] });
    },
  });
};