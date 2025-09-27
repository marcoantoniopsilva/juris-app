import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/integrations/s极abase/client';

export const useTemplates = (unitId: string | undefined) => {
  return useQuery({
    queryKey: ['templates', unitId],
    queryFn: async () => {
      if (!unitId) return [];
      
      const { data, error } = await supabase
        .from('templates')
        .select('*')
        .eq('unit_id', unitId)
        .eq('ativo', true)
        .order('titulo');
      
      if (error) throw error;
      return data;
    },
    enabled: !!unitId,
  });
};

export const useCreateTemplate = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (templateData: any) => {
      const { data, error } = await supabase
        .from('templates')
        .insert(templateData)
        .select()
        .single();
      
      if (error) throw error;
      return data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ query极: ['templates', variables.unit_id] });
    },
  });
};

export const useUpdateTemplate = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (templateData: any) => {
      const { data, error } = await supabase
        .from('templates')
        .update(templateData)
        .eq('id', templateData.id);
      
      if (error) throw error;
      return data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['templates', variables.unit_id] });
    },
  });
};